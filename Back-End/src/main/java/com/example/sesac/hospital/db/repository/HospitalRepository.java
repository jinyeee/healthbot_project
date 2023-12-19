package com.example.sesac.hospital.db.repository;

import com.example.sesac.hospital.db.entity.Hospital;
import org.springframework.data.jpa.repository.JpaRepository;

public interface HospitalRepository extends JpaRepository<Hospital, Long>, HospitalCustomRepository {
//    List<HospitalDepartment> findAllByHospitalDepartment(String hospitalDepartment);
}