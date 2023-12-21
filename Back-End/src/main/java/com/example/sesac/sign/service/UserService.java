package com.example.sesac.sign.service;

import com.example.sesac.sign.dto.LoginDto;
import com.example.sesac.sign.dto.UserDto;


public interface UserService {

    void createUser(UserDto userDto);

    UserDto loginUser(LoginDto loginDto);

    UserDto getUserInfo(Long userSequence);


}
