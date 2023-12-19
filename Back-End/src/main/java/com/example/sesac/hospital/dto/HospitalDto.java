package com.example.sesac.hospital.dto;

import lombok.Builder;
import lombok.Data;

@Data
public class HospitalDto {
    private Long hospitalId;
    private String hospitalName;
    private String hospitalAddress;
    private String hospitalCode;
    private String hospitalPost;
    private String hospitalTell;
    private double hospitalLongitude;
    private double hospitalLatitude;


    @Builder
    public HospitalDto(Long hospitalId, String hospitalName, String hospitalAddress
            , String hospitalCode, String hospitalPost, String hospitalTell
            , double hospitalLongitude, double hospitalLatitude) {
        this.hospitalId = hospitalId;
        this.hospitalName = hospitalName;
        this.hospitalAddress = hospitalAddress;
        this.hospitalCode = hospitalCode;
        this.hospitalPost = hospitalPost;
        this.hospitalTell = hospitalTell;
        this.hospitalLongitude = hospitalLongitude;
        this.hospitalLatitude = hospitalLatitude;
    }
}
