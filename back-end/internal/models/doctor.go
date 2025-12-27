package models

import "gorm.io/datatypes"

type Doctor struct {
	ID          uint           `gorm:"primaryKey" json:"id"`
	UserID      uint           `gorm:"unique" json:"user_id"`
	User        User           `gorm:"foreignKey:UserID" json:"user"`
	Specialty   string         `gorm:"size:100" json:"specialty"`
	VisitFee    int            `json:"visit_fee"`
	Schedule    datatypes.JSON `json:"schedule"` // e.g., working hours per day
	Rating      float64        `json:"rating,omitempty"`
	CreatedAt   string         `json:"created_at"`
	UpdatedAt   string         `json:"updated_at"`
}