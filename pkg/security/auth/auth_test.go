package auth

import (
	"testing"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/stretchr/testify/assert"
)

func TestGenerateToken(t *testing.T) {
	tokens, err := GenerateAuthTokens("grilario", time.Hour*3)

	assert.Nil(t, err)
	assert.NotNil(t, tokens)
	assert.Equal(t, 64, len(tokens.Refresh))
}

func TestVerifyAccessToken(t *testing.T) {
	t.Run("Valid jwt", func(t *testing.T) {
		tokens, _ := GenerateAuthTokens("grilario", time.Hour*3)
		ok, err := VerifyAccessToken(tokens.Access)

		assert.Nil(t, err)
		assert.True(t, ok)
	})

	t.Run("Invalid jwt", func(t *testing.T) {
		// other signing method
		token := jwt.NewWithClaims(jwt.SigningMethodHS384, jwt.MapClaims{
			"username": "grilario",
			"exp":      time.Now().Add(time.Hour * 3).Unix(),
		})

		accessToken, err := token.SignedString([]byte("secret"))
		ok, err := VerifyAccessToken(accessToken)

		assert.NotNil(t, err)
		assert.False(t, ok)
	})
}
