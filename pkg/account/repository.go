package account

type AccountRepository interface {
	Create(a *Account) (*Account, error)
}

type AccountMemoryRepo struct {
	accounts []Account
}

func (r *AccountMemoryRepo) Create(a *Account) (*Account, error) {
	r.accounts = append(r.accounts, *a)

	return a, nil
}
