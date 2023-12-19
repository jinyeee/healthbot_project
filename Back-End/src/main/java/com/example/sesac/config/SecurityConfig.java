//package com.example.sesac.config;
//import lombok.RequiredArgsConstructor;
//import org.springframework.context.annotation.Bean;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.security.config.annotation.web.builders.HttpSecurity;
//import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
//import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
//import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
//import org.springframework.security.config.annotation.web.configurers.FormLoginConfigurer;
//import org.springframework.security.config.annotation.web.configurers.HttpBasicConfigurer;
//import org.springframework.security.config.annotation.web.configurers.SessionManagementConfigurer;
//import org.springframework.security.config.http.SessionCreationPolicy;
//import org.springframework.security.web.SecurityFilterChain;
//import org.springframework.security.web.authentication.AuthenticationFailureHandler;
//import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
//
//@Configuration
//@EnableWebSecurity
//@RequiredArgsConstructor
//public class SecurityConfig {
//
//	private final CorsConfig corsConfig;
//	@Bean
//	public WebSecurityCustomizer webSecurityCustomizer() {
//		return (web) -> web.ignoring().requestMatchers("/tokens/reissue", "/swagger-ui/**", "/swagger-resources/**", "/v2/api-docs/**", "/favicon.ico");
//	}
//
//	@Bean
//	public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
//		http.httpBasic(HttpBasicConfigurer::disable)
//				.formLogin(FormLoginConfigurer::disable)
//				.csrf(CsrfConfigurer::disable)
//				.sessionManagement(session-> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
//				.logout(logout -> logout.logoutUrl("/logout").deleteCookies("accessToken", "refreshToken"))
//				.authorizeHttpRequests(request -> request
//						.requestMatchers("/favicon.ico").permitAll()
//						.requestMatchers("/sign").permitAll()
//						.anyRequest().authenticated()
//				)
//				.addFilter(corsConfig.corsFilter());
////				.addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider), UsernamePasswordAuthenticationFilter.class)
////				.addFilterBefore(new JwtExceptionFilter(), JwtAuthenticationFilter.class);
//		return http.build();
//	}
//}
