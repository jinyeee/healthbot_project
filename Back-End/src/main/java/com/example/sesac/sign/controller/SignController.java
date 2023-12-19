package com.example.sesac.sign.controller;


import com.example.sesac.sign.dto.LoginDto;
import com.example.sesac.sign.dto.LoginResp;
import com.example.sesac.sign.dto.UserDto;
import com.example.sesac.sign.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("sign")
@RequiredArgsConstructor
@Slf4j
public class SignController {
    private static final String SUCCESS = "success";
    private static final String FAIL = "fail";
    private final UserService userService;

    //회원 등록
    @PostMapping
    public ResponseEntity<String> createUser(@RequestBody UserDto userDto) {
        log.info("회원가입");
        userService.createUser(userDto);
        return new ResponseEntity<>(SUCCESS, HttpStatus.OK);

    }

    //로그인
    @PostMapping("login")
    public ResponseEntity<LoginResp> login(@RequestBody LoginDto loginDto) {
        log.info("로그인");
//        session = request.getSession();
        //System.out.print(loginDto);
        UserDto user = userService.loginUser(loginDto);
        if (user != null && user.getUserPw().equals(loginDto.getUserPw())) {
            //로그인 성공
//            session.setAttribute("userSequence", user.getUserSequence());
            log.info("로그인 성공");
            return new ResponseEntity<>(new LoginResp(SUCCESS, user.getUserSequence(), user.getUserId()), HttpStatus.OK);
        } else {
            log.info("로그인 실패");
            return new ResponseEntity<>(new LoginResp(FAIL), HttpStatus.OK);
        }

    }


    //로그인
//    @PostMapping("/login")
//    public ResponseEntity<Long> login(@RequestBody LoginDto loginDto, HttpSession session) {
////        session = request.getSession();
//        UserDto user = userService.loginUser(loginDto);
//        if (user != null && user.getUserPw().equals(loginDto.getUserPw())) {
//            //로그인 성공
//            session.setAttribute("userSequence", user.getUserSequence());
//            Object sequenceTest = session.getAttribute("userSequence");
//            Long userSequence = (Long) sequenceTest;
//            System.out.print(userSequence);
//            return new ResponseEntity<>(userSequence, HttpStatus.OK);
//        } else {
//            return new ResponseEntity<>(0L, HttpStatus.OK);
//        }
//
//    }


}
