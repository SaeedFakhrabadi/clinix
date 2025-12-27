package repositories

import (
	"clinic-appointment/internal/models"
	"time"

	"gorm.io/gorm"
)

type AppointmentRepository interface {
	Create(appointment *models.Appointment) error
	FindByID(id uint) (*models.Appointment, error)
	FindByDoctorAndTime(doctorID uint, dateTime time.Time) (*models.Appointment, error)
	GetByPatientID(patientID uint) ([]models.Appointment, error)
	GetByDoctorID(doctorID uint) ([]models.Appointment, error)
	Update(appointment *models.Appointment) error
	Delete(id uint) error
}

type appointmentRepository struct {
	db *gorm.DB
}

func NewAppointmentRepository(db *gorm.DB) AppointmentRepository {
	return &appointmentRepository{db: db}
}

func (r *appointmentRepository) Create(appointment *models.Appointment) error {
	return r.db.Create(appointment).Error
}

func (r *appointmentRepository) FindByID(id uint) (*models.Appointment, error) {
	var apt models.Appointment
	err := r.db.First(&apt, id).Error
	return &apt, err
}

func (r *appointmentRepository) FindByDoctorAndTime(doctorID uint, dateTime time.Time) (*models.Appointment, error) {
	var apt models.Appointment
	err := r.db.Where("doctor_id = ? AND date_time = ?", doctorID, dateTime).First(&apt).Error
	return &apt, err
}

func (r *appointmentRepository) GetByPatientID(patientID uint) ([]models.Appointment, error) {
	var appointments []models.Appointment
	err := r.db.Where("patient_id = ?", patientID).Find(&appointments).Error
	return appointments, err
}

func (r *appointmentRepository) GetByDoctorID(doctorID uint) ([]models.Appointment, error) {
	var appointments []models.Appointment
	err := r.db.Where("doctor_id = ?", doctorID).Find(&appointments).Error
	return appointments, err
}

func (r *appointmentRepository) Update(appointment *models.Appointment) error {
	return r.db.Save(appointment).Error
}

func (r *appointmentRepository) Delete(id uint) error {
	return r.db.Delete(&models.Appointment{}, id).Error
}