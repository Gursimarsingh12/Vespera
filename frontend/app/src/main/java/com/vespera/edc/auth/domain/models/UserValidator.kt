package com.vespera.edc.auth.domain.models

import android.util.Patterns
import java.text.ParseException
import java.text.SimpleDateFormat
import java.util.Locale

object UserValidator {
    fun validateEmail(email: String): String{
        return when {
            email.isEmpty() -> "*Required"
            !Patterns.EMAIL_ADDRESS.matcher(email).matches() -> "*Invalid Email"
            else -> ""
        }
    }

    fun validatePassword(password: String): String{
        val numRegex = Regex(".*[0-9].*")
        val charRegex = Regex(".*[a-z].*")
        val specialCharRegex = Regex(".*[^a-zA-Z0-9].*")
        val capitalCharRegex = Regex(".*[A-Z].*")
        return when{
            password.isEmpty() -> "*Required"
            password.length < 8 -> "It must have at least 8 characters"
            !numRegex.matches(password) -> "It must contain a number"
            !charRegex.matches(password) -> "It must contain a character"
            !specialCharRegex.matches(password) -> "It must contain a special character/symbol"
            !capitalCharRegex.matches(password) -> "It must contain a capital letter"
            else -> ""
        }
    }

    fun validateName(name: String): String{
        return when{
            name.isEmpty() -> "*Required"
            else -> ""
        }
    }

    fun validateDateFormat(date: String): String {
        val format = "yyyy-MM-dd"
        return try {
            val sdf = SimpleDateFormat(format, Locale.getDefault())
            sdf.isLenient = false
            sdf.parse(date)
            ""
        } catch (e: ParseException) {
            "*Invalid date format"
        }
    }
}