package com.example.sesac.review.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
public class HospitalReviewDto {

    private Long reviewId;
    private String hospitalName;
    private String content;

    @Builder
    public HospitalReviewDto(Long reviewId, String hospitalName, String content) {
        this.reviewId = reviewId;
        this.hospitalName = hospitalName;
        this.content = content;
    }
}
