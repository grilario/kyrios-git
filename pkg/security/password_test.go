package security

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPasswordHash(t *testing.T) {
	t.Run("Hashing", func(t *testing.T) {
		h := NewPasswordHash("hello", 512, 1, 1, 16, 32)
		hash, err := h.Hash("123")

		assert.Nil(t, err)
		assert.NotNil(t, hash)
		assert.Len(t, hash, 95)
	})

	t.Run("Compare", func(t *testing.T) {
		h := NewPasswordHash("hello", 512, 1, 1, 16, 32)

		hash, err := h.Hash("123")
		assert.Nil(t, err)

		{
			match, err := h.Compare("123467", hash)

			assert.Nil(t, err)
			assert.False(t, match)
		}
		{
			match, err := h.Compare("123", hash)

			assert.Nil(t, err)
			assert.True(t, match)
		}
	})
}
