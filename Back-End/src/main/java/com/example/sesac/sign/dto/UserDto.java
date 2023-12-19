package com.example.sesac.sign.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class UserDto {
    private Long userSequence;
    private String userId;
    private String userPw;
    private Integer userAge;
    private String userGender;

//    private String userName;
//    private String userEmail;
//    private String userAddr;
//    private String userTell;


    @Builder
    public UserDto(Long userSequence, String userId, String userPw
            , Integer userAge, String userGender) {
        this.userSequence = userSequence;
        this.userId = userId;
        this.userPw = userPw;
        this.userGender = userGender;
        this.userAge = userAge;
    }


}
