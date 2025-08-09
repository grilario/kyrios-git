package account

type AccountRepository interface {
	Create(a *Account) (*Account, error)
	GetByUsername(username string) (*Account, error)
	GetByEmail(email string) (*Account, error)
}

type ApiTokenRepository interface {
	Create(t *ApiToken) (*ApiToken, error)
}

type AccountMemoryRepo struct {
	accounts []Account
}

func (r *AccountMemoryRepo) Create(a *Account) (*Account, error) {
	r.accounts = append(r.accounts, *a)

	return a, nil
}

func (r *AccountMemoryRepo) GetByUsername(username string) (*Account, error) {
	return &Account{}, nil
}

func (r *AccountMemoryRepo) GetByEmail(email string) (*Account, error) {
	return &Account{}, nil
}
