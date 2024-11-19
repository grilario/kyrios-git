package util

import (
	"reflect"
	"strings"

	"github.com/go-playground/validator/v10"
)

func ValidateStruct(s interface{}, validate *validator.Validate, messageErrors map[string]string) []map[string]string {
	err := validate.Struct(s)

	if err == nil {
		return nil
	}

	errs := err.(validator.ValidationErrors)
	var errsMap []map[string]string

	for _, err := range errs {
		e := make(map[string]string)

		e["field"] = err.Field()
		e["type"] = err.Type().Name()
		e["message"] = messageErrors[e["field"]]

		errsMap = append(errsMap, e)
	}

	return errsMap
}

func GetJsonFieldName(fld reflect.StructField) string {
	name := strings.SplitN(fld.Tag.Get("json"), ",", 2)[0]
	if name == "-" {
		return ""
	}
	return name
}
