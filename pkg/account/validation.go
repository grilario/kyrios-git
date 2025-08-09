package account

import (
	"errors"
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
		"username":       "username must be between 2 and 30 lowercase alphanumeric characters or '.' and '_'",
		"name":           "name must be between 8 and 150 characters",
		"email":          "email must be valid",
		"password":       "password must be at least 8 characters and contain one lowercase letter, one uppercase letter, a number and a symbol",
		"identification": "identification must be username or email",
		"user_agent":     "user_agent is required",
		"ip_address":     "ip_address must be valid ip",
	}
)

func (a *NewAccount) Validate() []map[string]string {
	return util.ValidateStruct(a, validate, accountErrors)
}

func (a *LoginDetails) Validate() []map[string]string {
	return util.ValidateStruct(a, validate, accountErrors)
}

func ValidateIdentification(identification string) (username, email interface{}, error error) {
	err := validate.Var(identification, "required,email")
	if err == nil {
		return nil, identification, nil
	}

	err = validate.Var(identification, "required,min=2,max=30,username")
	if err == nil {
		return identification, nil, nil
	}

	return nil, nil, errors.New("invalid credentials")
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
