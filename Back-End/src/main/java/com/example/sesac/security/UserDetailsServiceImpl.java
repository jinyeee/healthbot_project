//package com.example.sesac.security;
//
//import com.example.sesac.sign.db.entity.User;
//import com.example.sesac.sign.db.repository.UserRepository;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.security.core.userdetails.UserDetails;
//import org.springframework.security.core.userdetails.UserDetailsService;
//import org.springframework.security.core.userdetails.UsernameNotFoundException;
//import org.springframework.stereotype.Service;
//
//@Service("userDetailsService")
//@Configuration
//public class UserDetailsServiceImpl implements UserDetailsService {
//    private UserRepository repository;
//
//    //시큐리티 session(Authentication(내부 UserDetails))
//    // 함수 종료 시 @AuthenticationPrincipal 이 만들어진다.
//    @Override
//    public UserDetails loadUserByUsername(String userId) throws UsernameNotFoundException {
//        User userEntity = repository.findByUserId(userId).orElse(null);
//
//        if (userEntity != null)
//            return new PrincipalDetails(userEntity);
//
//        return null;
//    }
//}
