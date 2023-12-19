package com.example.sesac.sign.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class LoginResp {
    String result;
    Long userSeq;
    String userId;

    public LoginResp(String result, Long userSeq, String userId) {
        this.result = result;
        this.userSeq = userSeq;
        this.userId = userId;
    }

    public LoginResp(String result) {
        this.result = result;
    }
}
