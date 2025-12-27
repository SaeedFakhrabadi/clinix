package models

import "time"

type AppointmentStatus string

const (
	StatusPending   AppointmentStatus = "pending"
	StatusConfirmed AppointmentStatus = "confirmed"
	StatusCancelled AppointmentStatus = "cancelled"
)

type Appointment struct {
	ID         uint              `gorm:"primaryKey" json:"id"`
	PatientID  uint              `json:"patient_id"`
	DoctorID   uint              `json:"doctor_id"`
	DateTime   time.Time         `json:"date_time"`
	Status     AppointmentStatus `gorm:"default:pending" json:"status"`
	CreatedAt  time.Time         `json:"created_at"`
	UpdatedAt  time.Time         `json:"updated_at"`
}