package account_test

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
	"go.uber.org/mock/gomock"

	. "github.com/grilario/kyrios-git/pkg/account"
)

func TestCreateAccount(t *testing.T) {
	t.Run("Fail validation", func(t *testing.T) {
		r := AccountMemoryRepo{}

		a := Create(NewAccount{"f", "Luis Fernando", "any@anyany", "123"}, &r)

		assert.NotNil(t, a.Errors)
		assert.Equal(t, a.Status, 422)
	})

	t.Run("Success", func(t *testing.T) {
		r := AccountMemoryRepo{}

		a := Create(NewAccount{"grilario", "Luis Fernando", "any@any.any", "#@!He123*!"}, &r)

		assert.NotNil(t, a.Data)
		assert.Equal(t, a.Status, 201)

		var aOut map[string]any
		j, _ := json.Marshal(a.Data)
		err := json.Unmarshal(j, &aOut)

		assert.Nil(t, err)
		assert.Nil(t, aOut["password"])
	})
}

func TestLogin(t *testing.T) {
	ctrl := gomock.NewController(t)

	d := LoginDetails{
		Identification: "grilario",
		Password:       "123",
		UserAgent:      "any",
		IpAddress:      "192.168.0.1",
	}

	accountRepo := NewMockAccountRepository(ctrl)
	apiTokenRepo := NewMockApiTokenRepository(ctrl)

	hash := "$argon2id$v=19$m=16,t=2,p=1$M0xIczd4TXR6UEdkeGJWYg$gpgVW6d0mri82UJE7XnqAA" // hash for 123 with secret 'secret'
	accountRepo.
		EXPECT().
		GetByUsername(gomock.Eq("grilario")).
		Return(&Account{Username: "grilario", Password: hash}, nil)

	apiTokenRepo.
		EXPECT().
		Create(gomock.Any()).
		DoAndReturn(func(t *ApiToken) (interface{}, error) {
			return t, nil
		})

	r := Login(d, accountRepo, apiTokenRepo)
	assert.Nil(t, r.Errors)

	var bodyOut map[string]any
	jsonBody, err := json.Marshal(r.Data)
	json.Unmarshal(jsonBody, &bodyOut)

	assert.Nil(t, err)
	assert.NotNil(t, bodyOut["refresh_token"])
	assert.NotNil(t, bodyOut["access_token"])
}
