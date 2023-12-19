package com.example.sesac.mypage.controller;

import com.example.sesac.sign.dto.UserDto;
import com.example.sesac.sign.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("mypage")
public class MypageController {

    private final UserService userService;

    //회원 정보 조회
    //sequence로 구현해두고 추후에 token으로 변경 예정.
    @GetMapping("{userSequence}")
    public ResponseEntity<UserDto> getUserInfo(@PathVariable(name = "userSequence") Long userSequence) {
        return new ResponseEntity<>(userService.getUserInfo(userSequence), HttpStatus.OK);

    }

//    @PostMapping
//    public ResponseEntity<UserDto> getUserInfo(@PathVariable Long userSequence) {
//        return new ResponseEntity<>(userService.getUserInfo(userSequence), HttpStatus.OK);
//
//    }


}
