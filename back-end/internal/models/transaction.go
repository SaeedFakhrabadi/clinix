package models

import "time"

type TransactionType string

const (
	TransactionPayment TransactionType = "payment"
	TransactionRefund  TransactionType = "refund"
)

type Transaction struct {
	ID            uint            `gorm:"primaryKey" json:"id"`
	AppointmentID uint            `json:"appointment_id,omitempty"`
	PatientID     uint            `json:"patient_id"`
	Amount        int             `json:"amount"` // in Rials or Toman
	Type          TransactionType `gorm:"type:varchar(20)" json:"type"`
	Status        string          `gorm:"size:50" json:"status"` // success, failed, pending
	Gateway       string          `gorm:"size:100" json:"gateway,omitempty"`
	TrackingCode  string          `gorm:"size:100" json:"tracking_code,omitempty"`
	CreatedAt     time.Time       `json:"created_at"`
	UpdatedAt     time.Time       `json:"updated_at"`
}