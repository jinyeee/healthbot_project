package com.example.sesac.sign.service.impl;

import com.example.sesac.sign.db.entity.User;
import com.example.sesac.sign.db.repository.UserRepository;
import com.example.sesac.sign.dto.LoginDto;
import com.example.sesac.sign.dto.UserDto;
import com.example.sesac.sign.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    @Override
    public void createUser(UserDto userDto) {
        userRepository.save(User.toEntity(userDto));

    }

    @Override
    public UserDto loginUser(LoginDto loginDto) {
        return userRepository.findByUserId(loginDto.getUserId()).map(User::toDto).orElse(null);
    }


    @Override
    public UserDto getUserInfo(Long userSequence) {
        return userRepository.findById(userSequence).map(User::toDto).orElse(null);
    }


    //*****<로그인 기능 추가 예정>*******
    //    @Override
//    public boolean loginResult(LoginDto loginDto){
//        User user = userRepository.findByUserId(loginDto.getUserId()).map(User::toDto).orElse(null);
//        if(user != null && user.getUserPw().equals(loginDto.getUserPw())){
//            //로그인 성공a
//            String True = "True";
//            return True;
//        }else {
//            String False = "false";
//            return False;
//        }
//    }


}
