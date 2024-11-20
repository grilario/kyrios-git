package account

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
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

		j, _ := json.MarshalIndent(a.Data, "", "\t")

		var aOut map[string]any
		err := json.Unmarshal(j, &aOut)

		assert.Nil(t, err)
		assert.Nil(t, aOut["password"])
	})
}
