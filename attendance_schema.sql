--
-- Create model Faculty
--
CREATE TABLE `attendance_faculty` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `faculty_id` varchar(10) NOT NULL UNIQUE, `name` varchar(100) NOT NULL, `email` varchar(254) NOT NULL UNIQUE);
--
-- Create model Student
--
CREATE TABLE `attendance_student` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `student_id` varchar(10) NOT NULL UNIQUE, `name` varchar(100) NOT NULL, `year` integer NOT NULL, `semester` integer NOT NULL);
--
-- Create model Subject
--
CREATE TABLE `attendance_subject` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `subject_code` varchar(10) NOT NULL UNIQUE, `name` varchar(100) NOT NULL, `year` integer NOT NULL, `semester` integer NOT NULL, `faculty_id` bigint NULL);
--
-- Create model Attendance
--
CREATE TABLE `attendance_attendance` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `date` date NOT NULL, `period` integer NOT NULL, `status` varchar(10) NOT NULL, `student_id` bigint NOT NULL, `subject_id` bigint NOT NULL);
anc` FOREIGN KEY (`student_id`) REFERENCES `attendance_student` (`id`);
ALTER TABLE `attendance_attendance` ADD CONSTRAINT `attendance_attendanc_subject_id_624b6d52_fk_attendanc` FOREIGN KEY (`subject_id`) REFERENCES `attendance_subject` (`id`);