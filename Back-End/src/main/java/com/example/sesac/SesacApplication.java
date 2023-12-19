package com.example.sesac;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class SesacApplication {

    public static void main(String[] args) {
        SpringApplication.run(SesacApplication.class, args);
    }

}
