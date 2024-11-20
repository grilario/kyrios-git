package account

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewAccount(t *testing.T) {

	t.Run("Valid Accounts", func(t *testing.T) {
		assert := assert.New(t)

		accounts := []NewAccount{
			{Username: "grilo", Name: "Luis Fernando", Email: "any@any.any", Password: "A123456b$"},
			{Username: "cri.cri", Name: "Fernandinho", Email: "ola@gmail.com", Password: "Oche123!"},
			{Username: "cri_cri", Name: "Foobar 123", Email: "hhe432@gmail.com", Password: "#@!Haha13#@!*"},
		}

		for _, a := range accounts {
			err := a.Validate()
			assert.Nilf(err, "error: %v \naccount: %+v", err, a)
		}
	})

	t.Run("Invalid Accounts", func(t *testing.T) {
		assert := assert.New(t)

		accounts := []NewAccount{
			{Username: "grilo-", Name: "Luis Fernando", Email: "any@any.any", Password: "A123456b$"},
			{Username: "cri.cri", Name: "Grilo", Email: "ola@gmail.com", Password: "Oche123!"},
			{Username: "cri_cri", Name: "Foobar 123", Email: "hhe432@gmailcom", Password: "#@!Haha13#@!*"},
			{Username: "cri_cri", Name: "Foobar 123", Email: "hhe432@gmailcom", Password: "Hehehehe"},
		}

		for _, a := range accounts {
			err := a.Validate()
			assert.NotNilf(err, "account: %+v", a)
		}
	})
}
