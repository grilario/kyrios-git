package account

//go:generate go tool mockgen -destination account_mock_test.go -package account_test . AccountRepository,ApiTokenRepository

import (
	"time"

	"github.com/grilario/kyrios-git/pkg/security"
	"github.com/grilario/kyrios-git/pkg/security/auth"
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

type ApiToken struct {
	RefreshToken string
	Username     string
	UserAgent    string
	IpAddress    string
	CreatedAt    time.Time
	UpdatedAt    time.Time
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

type LoginDetails struct {
	Identification string `json:"identification" validate:"required"`
	Password       string `json:"password" validate:"required"`
	UserAgent      string `json:"user_agent" validate:"required"`
	IpAddress      string `json:"ip_address" validate:"required,ip_addr"`
}

func Login(d LoginDetails, accountRepo AccountRepository, tokenRepo ApiTokenRepository) Reply {
	if err := d.Validate(); err != nil {
		return Reply{Status: 422, Errors: err}
	}

	username, email, err := ValidateIdentification(d.Identification)
	if err != nil {
		return Reply{Status: 403, Errors: []string{"invalid credentials"}}
	}

	var account *Account
	if username != nil {
		account, err = accountRepo.GetByUsername(username.(string))
		if err != nil {
			return Reply{Status: 403, Errors: []string{"invalid credentials"}}
		}
	} else {
		account, err = accountRepo.GetByEmail(email.(string))
		if err != nil {
			return Reply{Status: 403, Errors: []string{"invalid credentials"}}
		}
	}

	h := security.GetPasswordHashInstance()
	match, err := h.Compare(d.Password, account.Password)

	if err != nil {
		return Reply{Status: 500, Errors: []string{"internal server error"}}
	}
	if !match {
		return Reply{Status: 403, Errors: []string{"invalid credentials"}}
	}

	twoMonths := time.Hour * 24 * 30 * 2
	tokens, err := auth.GenerateAuthTokens(account.Username, twoMonths)
	if err != nil {
		return Reply{Status: 500, Errors: []string{"internal server error"}}
	}

	t := &ApiToken{
		RefreshToken: tokens.Refresh,
		Username:     account.Username,
		UserAgent:    d.UserAgent,
		IpAddress:    d.IpAddress,
		CreatedAt:    time.Now().UTC(),
		UpdatedAt:    time.Now().UTC(),
	}

	t, err = tokenRepo.Create(t)
	if err != nil {
		return Reply{Status: 500, Errors: []string{"internal server error"}}
	}

	return Reply{Status: 200, Data: tokens}
}
