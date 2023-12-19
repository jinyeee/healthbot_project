package com.example.sesac.hospital.db.repository;

import com.example.sesac.hospital.dto.HospitalDepReq;
import com.example.sesac.hospital.dto.HospitalReviewSumDto;

import java.util.List;

public interface HospitalCustomRepository {
    List<HospitalReviewSumDto> getHospital(HospitalDepReq hospitalDepReq);
}
