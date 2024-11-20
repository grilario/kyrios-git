package account

import (
	"time"

	"github.com/grilario/kyrios-git/pkg/security"
	. "github.com/grilario/kyrios-git/pkg/util/api"
)

type Account struct {
	Username  string    `json:"username"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	Password  string    `json:"-"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type NewAccount struct {
	Username string `json:"username" validate:"required,min=2,max=30,username"`
	Name     string `json:"name" validate:"required,min=8,max=150"`
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required,min=8,max=80,password"`
}

func Create(a NewAccount, r AccountRepository) Reply {
	if err := a.Validate(); err != nil {
		return Reply{Status: 422, Errors: err}
	}

	h := security.GetPasswordHashInstance()

	p, err := h.Hash(a.Password)
	if err != nil {
		return Reply{Status: 500, Errors: []string{"internal server error"}}
	}

	acc := &Account{
		Username:  a.Username,
		Name:      a.Name,
		Email:     a.Email,
		Password:  p,
		CreatedAt: time.Now().UTC(),
		UpdatedAt: time.Now().UTC(),
	}

	acc, err = r.Create(acc)
	if err != nil {
		return Reply{Status: 500, Errors: []string{"internal server error"}}
	}

	return Reply{Status: 201, Data: acc}
}
