package auth

import (
	"crypto/rand"
	"encoding/base64"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

type AuthToken struct {
	Refresh string `json:"refresh_token"`
	Access  string `json:"access_token"`
}

func GenerateAuthTokens(username string, expiration time.Duration) (AuthToken, error) {
	accessToken, err := GenerateAccessToken(username, expiration)
	if err != nil {
		return AuthToken{}, err
	}

	b, err := randomBytes(48)
	if err != nil {
		return AuthToken{}, err
	}
	refreshToken := base64.RawURLEncoding.EncodeToString(b)

	return AuthToken{refreshToken, accessToken}, nil
}

func GenerateAccessToken(username string, expiration time.Duration) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"username": username,
		"exp":      time.Now().Add(expiration).Unix(),
	})

	accessToken, err := token.SignedString([]byte("secret"))
	if err != nil {
		return "", err
	}

	return accessToken, nil
}

func VerifyAccessToken(token string) (bool, error) {
	t, err := jwt.Parse(token, func(t *jwt.Token) (interface{}, error) {
		return []byte("secret"), nil
	}, jwt.WithValidMethods([]string{"HS256"}))

	if err != nil {
		return false, err
	}

	return t.Valid, nil
}

func randomBytes(n uint32) ([]byte, error) {
	b := make([]byte, n)
	_, err := rand.Read(b)
	if err != nil {
		return nil, err
	}

	return b, nil
}
