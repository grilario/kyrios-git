package account

import (
	"unicode"

	"github.com/grilario/kyrios-git/pkg/util"

	"github.com/go-playground/validator/v10"
)

func init() {
	validate = validator.New(validator.WithRequiredStructEnabled())
	validate.RegisterTagNameFunc(util.GetJsonFieldName)

	validate.RegisterValidation("username", validateUsername)
	validate.RegisterValidation("password", validatePassword)
}

var (
	validate      *validator.Validate
	accountErrors = map[string]string{
		"username": "username must be between 2 and 30 lowercase alphanumeric characters or '.' and '_'",
		"name":     "name must be between 8 and 150 characters",
		"email":    "email must be valid",
		"password": "password must be at least 8 characters and contain one lowercase letter, one uppercase letter, a number and a symbol",
	}
)

type NewAccount struct {
	Username string `json:"username" validate:"required,min=2,max=30,username"`
	Name     string `json:"name" validate:"required,min=8,max=150"`
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required,min=8,max=80,password"`
}

func (a *NewAccount) Validate() []map[string]string {
	return util.ValidateStruct(a, validate, accountErrors)
}

// check if characters is alphanumeric or '_' or '.'
func validateUsername(f validator.FieldLevel) bool {
	u := f.Field().String()

	for _, r := range u {
		if r == '.' || r == '_' {
			return true
		}
		if r > unicode.MaxASCII || !(unicode.IsLetter(r) && unicode.IsLower(r)) && !unicode.IsDigit(r) {
			return false
		}
	}
	return true
}

// check if password contains at least one upper letter, one lower letter, one digit, one symbol
func validatePassword(f validator.FieldLevel) bool {
	p := f.Field().String()

	var hasUpper, hasLower, hasNumber, hasSymbol bool

	for _, r := range p {
		switch {
		case unicode.IsUpper(r):
			hasUpper = true
		case unicode.IsLower(r):
			hasLower = true
		case unicode.IsDigit(r):
			hasNumber = true
		case unicode.IsPunct(r) || unicode.IsSymbol(r):
			hasSymbol = true
		}

		if hasUpper && hasLower && hasNumber && hasSymbol {
			return true
		}
	}

	return hasUpper && hasLower && hasNumber && hasSymbol
}
