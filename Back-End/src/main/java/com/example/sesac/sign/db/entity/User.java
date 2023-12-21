package com.example.sesac.sign.db.entity;


import com.example.sesac.sign.dto.UserDto;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Entity
@NoArgsConstructor
@Getter
@Slf4j
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long userSequence;
    private String userId;
    private String userPw;
    private Integer userAge;
    private String userGender;

    @Builder
    public User(String userId, String userPw
            , Integer userAge, String userGender) {
        this.userId = userId;
        this.userPw = userPw;
        this.userAge = userAge;
        this.userGender = userGender;
    }

    public static UserDto toDto(User user) {
        return UserDto.builder()
                .userSequence(user.getUserSequence())
                .userId(user.getUserId())
                .userPw(user.getUserPw())
                .userAge(user.getUserAge())
                .userGender(user.getUserGender())
                .build();
    }

    public static User toEntity(UserDto userDto) {
        return User.builder()
                .userId(userDto.getUserId())
                .userPw(userDto.getUserPw())
                .userAge(userDto.getUserAge())
                .userGender(userDto.getUserGender())
                .build();
    }


}
