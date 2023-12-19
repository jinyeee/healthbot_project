package com.example.sesac.sign.db.repository;

import com.example.sesac.sign.db.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUserId(String userId);


    //jpa에 기본으로 있는 함수는 커스텀하지 않고 그대로 가져와서 사용
    //없는 함수는 커스텀으로 생성해서 사용해야 한다.
//    Optional<User> getUserInfo(String userId);


}
