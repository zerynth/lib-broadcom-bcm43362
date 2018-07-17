/*
    ChibiOS/RT - Copyright (C) 2006-2013 Giovanni Di Sirio

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
/*
 * **** This file incorporates work covered by the following copyright and ****
 * **** permission notice:                                                 ****
 *
 * Copyright (c) 2001-2004 Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
 * SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
 * IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
 * OF SUCH DAMAGE.
 *
 * This file is part of the lwIP TCP/IP stack.
 *
 * Author: Adam Dunkels <adam@sics.se>
 *
 */

// see http://lwip.wikia.com/wiki/Porting_for_an_OS for instructions

#include "lwip/opt.h"
#include "lwip/mem.h"
#include "lwip/sys.h"
#include "lwip/stats.h"

#include "arch/cc.h"
#include "arch/sys_arch.h"

//extern VSemaphore tsem;
//#define zprintf(...) do { vosSemWait(tsem); vbl_printf_stdout(__VA_ARGS__); vosThSleep(TIME_U(10,MILLIS)); vosSemSignal(tsem);} while(0)

//#define zprintf(...) vbl_printf_stdout(__VA_ARGS__)
//#define zprintf(...)

#if defined(BCM43362__TEST_LWIP)
    #define printf(...) vbl_printf_stdout(__VA_ARGS__)
    #define zprintf(...) vbl_printf_stdout(__VA_ARGS__)
    #define WPRINT_WWD_ERROR(x) zprintf("Error %s",x)
    #define wiced_assert(x,c) if (!(c)) {zprintf(x);}
#else
    #define printf(...)
    #define zprintf(...)
    #define WPRINT_WWD_ERROR(x)
    #define wiced_assert(x,c)
#endif


int errno;

void sys_init(void) {

}

err_t sys_sem_new(sys_sem_t *sem, u8_t count) {
    *sem = vosSemCreate(count);
    return ERR_OK;
}

void sys_sem_free(sys_sem_t *sem) {
  vosSemDestroy(*sem);
}

void sys_sem_signal(sys_sem_t *sem) {
  vosSemSignal(*sem);
}

u32_t sys_arch_sem_wait(sys_sem_t *sem, u32_t timeout) {
  u32_t now = _systime_millis;
  int ret = vosSemWaitTimeout(*sem,(timeout==0) ? (VTIME_INFINITE):(TIME_U(timeout,MILLIS)));
  if(ret==VRES_OK)
    return (_systime_millis-now);
  else
    return SYS_ARCH_TIMEOUT;
}

int sys_sem_valid(sys_sem_t *sem) {
  return *sem != SYS_SEM_NULL;
}

// typically called within lwIP after freeing a semaphore
// to make sure the pointer is not left pointing to invalid data
void sys_sem_set_invalid(sys_sem_t *sem) {
  *sem = SYS_SEM_NULL;
}

err_t sys_mbox_new(sys_mbox_t *mbox, int size) {
    *mbox = vosMBoxCreate((size>0) ? size:1) ;
    zprintf("new mailbox %x of %i\n",*mbox,size);
    return ERR_OK;
}

void sys_mbox_free(sys_mbox_t *mbox) {
  zprintf("destroy mailbox %x\n",*mbox);
  vosMBoxDestroy(*mbox);
}

void sys_mbox_post(sys_mbox_t *mbox, void *msg) {
  zprintf("posting to mailbox %x msg %x\n",*mbox,msg);
  vosMBoxPost(*mbox,msg);
}

err_t sys_mbox_trypost(sys_mbox_t *mbox, void *msg) {
  zprintf("try posting to mailbox %x msg %x\n",*mbox,msg);
  vosSysLock();
  int slots = vosMBoxFreeSlots(*mbox);
  if(slots>0){
    vosMBoxPostIsr(*mbox,msg);
    slots = ERR_OK; 
  } else {
    slots = ERR_MEM;
  }
  vosSysUnlock();
  zprintf("tr posting to mailbox %x with result %i\n",*mbox,slots);
  return slots;
}

u32_t sys_arch_mbox_fetch(sys_mbox_t *mbox, void **msg, u32_t timeout) {
  u32_t now = _systime_millis;
  void *themsg;
  zprintf("fetching from mailbox %x timeout %x on msg %x\n",*mbox,timeout,msg);
  int ret = vosMBoxFetchTimeout(*mbox,&themsg,(timeout==0) ? (VTIME_INFINITE):(TIME_U(timeout,MILLIS)));
  zprintf("fetched from mailbox %x msg %x after %i/%i res %i\n",*mbox,themsg,(_systime_millis-now),timeout,ret);
  if(msg)
    *msg=themsg;
  if(ret==VRES_OK)
    return (_systime_millis-now);
  else
    return SYS_ARCH_TIMEOUT;
}

u32_t sys_arch_mbox_tryfetch(sys_mbox_t *mbox, void **msg) {
  zprintf("try fetching from mailbox %x\n",*mbox); 
  vosSysLock();
  /*int slots = vosMBoxUsedSlots(*mbox);
  if(slots>0){
    vosMBoxFetchIsr(*mbox,msg);
    slots = ERR_OK; 
  } else {
    slots = SYS_MBOX_EMPTY;
  }*/
  void *themsg;
  int slots = vosMBoxFetchIsr(*mbox,&themsg);
  vosSysUnlock();
  if(msg)
    *msg=themsg;
  zprintf("try fetching from mailbox %x with result %i %x\n",*mbox,slots,themsg); 
  return (slots<0) ? SYS_MBOX_EMPTY:ERR_OK;
}

int sys_mbox_valid(sys_mbox_t *mbox) {
  return *mbox != SYS_MBOX_NULL;
}

// typically called within lwIP after freeing an mbox
// to make sure the pointer is not left pointing to invalid data
void sys_mbox_set_invalid(sys_mbox_t *mbox) {
  *mbox = SYS_MBOX_NULL;
}

sys_thread_t sys_thread_new(const char *name, lwip_thread_fn thread,
                            void *arg, int stacksize, int prio) {
  VThread th = vosThCreate(stacksize,prio,thread,arg,NULL);
  vosThResume(th);
  return th;
}

sys_prot_t sys_arch_protect(void) {
  vosSysLock();
  return 1;
}

void sys_arch_unprotect(sys_prot_t pval) {
  vosSysUnlock();
}

u32_t sys_now(void) {

  return _systime_millis;
}

void sys_thread_exit( void )
{
}

void sys_thread_free( sys_thread_t task ){
  zprintf("Destroying thread %x\n",task);
  vosThDestroy(task);
}

uint16_t sys_rand16( void )
{
    /*uint16_t output;
    wwd_wifi_get_random( &output, 2 );
    return output;*/
    return 42;
}

void
sys_msleep(u32_t ms)
{
  vosThSleep(TIME_U(ms, MILLIS));
}

void sys_deinit( void )
{
}
