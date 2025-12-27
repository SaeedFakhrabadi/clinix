package handlers

import (
	"./internal/models"
	"./internal/services"
	"net/http"

	"github.com/gin-gonic/gin"
)

// AdminHandler handles admin-related endpoints
type AdminHandler struct {
	userService      services.UserService
	doctorService    services.DoctorService
	appointmentService services.AppointmentService
}

// NewAdminHandler creates a new AdminHandler
func NewAdminHandler(
	userService services.UserService,
	doctorService services.DoctorService,
	appointmentService services.AppointmentService,
) *AdminHandler {
	return &AdminHandler{
		userService:      userService,
		doctorService:    doctorService,
		appointmentService: appointmentService,
	}
}

// Example: Get all users (for admin dashboard)
// GET /admin/users
func (h *AdminHandler) GetUsers(c *gin.Context) {
	users, err := h.userService.GetAllUsers()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch users"})
		return
	}
	c.JSON(http.StatusOK, users)
}

// TODO: Add more admin endpoints later
// - Manage doctors
// - View reports
// - Manage transactions
// - etc.