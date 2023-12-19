package com.example.sesac.review.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
public class ReviewSumDto {
    private Long sumId;
    private Long hospitalId;
    private String hospitalName;
    private Long positiveReviewCnt;
    private Long negativeReviewCnt;
    private Long reviewTotalCnt;
    private Double positivePercentage;
    private Double negativePercentage;

    @Builder
    public ReviewSumDto(Long sumId, Long hospitalId, String hospitalName
            , Long positiveReviewCnt, Long negativeReviewCnt, Long reviewTotalCnt
            , Double positivePercentage, Double negativePercentage) {
        this.sumId = sumId;
        this.hospitalId = hospitalId;
        this.hospitalName = hospitalName;
        this.positiveReviewCnt = positiveReviewCnt;
        this.negativeReviewCnt = negativeReviewCnt;
        this.reviewTotalCnt = reviewTotalCnt;
        this.positivePercentage = positivePercentage;
        this.negativePercentage = negativePercentage;
    }
}

