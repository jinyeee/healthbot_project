package com.example.sesac.hospital.service;

import com.example.sesac.hospital.dto.HospitalDepReq;
import com.example.sesac.hospital.dto.HospitalDto;
import com.example.sesac.hospital.dto.HospitalReviewSumDto;

import java.util.List;

public interface HospitalService {

    HospitalDto getHospital(Long hospitalId);

    List<HospitalDto> getAll();

    //병원 정보 리스트 조회(진료과 기준)
    List<HospitalReviewSumDto> getHospitalList(HospitalDepReq hospitalDepReq);
}
