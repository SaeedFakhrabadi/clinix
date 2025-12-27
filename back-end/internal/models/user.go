package models

import "time"

type Role string

const (
	RolePatient Role = "patient"
	RoleDoctor  Role = "doctor"
	RoleAdmin   Role = "admin"
)

type User struct {
	ID        uint      `gorm:"primaryKey" json:"id"`
	Name      string    `gorm:"size:100" json:"name"`
	Phone     string    `gorm:"unique;size:20" json:"phone"`
	Email     string    `gorm:"unique;size:100" json:"email,omitempty"`
	Password  string    `gorm:"size:255" json:"-"`
	Role      Role      `gorm:"type:varchar(20);default:patient" json:"role"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}