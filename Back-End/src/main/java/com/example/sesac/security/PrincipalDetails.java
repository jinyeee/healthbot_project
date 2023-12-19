//package com.example.sesac.security;
//
//import com.example.sesac.sign.db.entity.User;
//import lombok.Data;
//import org.springframework.security.core.GrantedAuthority;
//import org.springframework.security.core.userdetails.UserDetails;
//
//import java.util.ArrayList;
//import java.util.Collection;
//import java.util.Map;
//
////시큐리티가 /login을 주소 요청이 오면 낚아채서 로그인 진행
////로그인을 진행이 완료가 되면 시큐리티 session을 만들어줌 (Security ContextHolder 라는 곳에 저장)
////저장 되는 오브젝트 => Authentication 타입의 객체
//// Authentication 안에 User 정보가 있어야함
//// User 오브젝트의 타입 => UserDetails 타입 객체여야함
//// 즉, Security Session => Authentication => UserDetails(PrincipalDetails)
//@Data
//public class PrincipalDetails implements UserDetails {
//
//    private User user;
//    private Map<String, Object> attributes;
//
//    //일반 로그인 할 때 사용
//    public PrincipalDetails(User user) {
//        this.user = user;
//    }
//
//
//    //해당 User 권한을 리턴
//    @Override
//    public Collection<? extends GrantedAuthority> getAuthorities() {
//        Collection<GrantedAuthority> collection = new ArrayList<>();
//        collection.add((GrantedAuthority) () -> user.getRole());
//        return collection;
//    }
//
//    @Override
//    public String getPassword() {
//        return user.getUserPw();
//    }
//
//    @Override
//    public String getUsername() {
//        return user.getUserId();
//    }
//
//    @Override
//    public boolean isAccountNonExpired() {
//        return true;
//    }
//
//    @Override
//    public boolean isAccountNonLocked() {
//        return true;
//    }
//
//    @Override
//    public boolean isCredentialsNonExpired() {
//        return true;
//    }
//
//    @Override
//    public boolean isEnabled() {
//        //장기 미로그인 유저 판단할 때
//        //현재시간 - 로그인 시간 => 1년을 초과하면 false설정
//        return true;
//    }
//}
//
