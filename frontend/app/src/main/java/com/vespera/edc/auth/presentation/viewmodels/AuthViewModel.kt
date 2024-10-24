package com.vespera.edc.auth.presentation.viewmodels

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.google.firebase.auth.FirebaseUser
import com.vespera.edc.auth.domain.models.UserState
import com.vespera.edc.auth.domain.models.UserValidator
import com.vespera.edc.auth.domain.repository.AuthRepository
import com.vespera.edc.core.models.User
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class AuthViewModel(
    private val repository: AuthRepository
): ViewModel() {
    private val _authState = MutableStateFlow(UserState<FirebaseUser>())
    val authState: StateFlow<UserState<FirebaseUser>> = _authState.asStateFlow()

    fun onEmailChange(email: String) {
        _authState.update {
            it.copy(
                email = email,
                emailError = UserValidator.validateEmail(email)
            )
        }
    }

    fun onPasswordChange(password: String) {
        _authState.update {
            it.copy(
                password = password,
                passwordError = UserValidator.validatePassword(password)
            )
        }
    }

    fun onPassWordVisible() {
        _authState.update {
            it.copy(
                isPasswordVisible = !it.isPasswordVisible
            )
        }
    }

    fun signUp() {
        if (isValidInput()) {
            val user = User(
                email = _authState.value.email,
                password = _authState.value.password,
                name = authState.value.name
            )
            viewModelScope.launch {
                repository.register(user).collectLatest { state ->
                    _authState.update {
                        it.copy(
                            state = state
                        )
                    }
                }
            }
        }
    }

    fun signIn() {
        if (isValidInput()) {
            val user = User(
                email = _authState.value.email,
                password = _authState.value.password
            )
            viewModelScope.launch {
                repository.logIn(user).collectLatest { state ->
                    _authState.update {
                        it.copy(
                            state = state
                        )
                    }
                }
            }
        }
    }

    private fun isValidInput(): Boolean {
        val emailError = UserValidator.validateEmail(_authState.value.email)
        val passwordError = UserValidator.validatePassword(_authState.value.password)
        _authState.update {
            it.copy(
                emailError = emailError,
                passwordError = passwordError
            )
        }
        return emailError.isEmpty() && passwordError.isEmpty()
    }

    fun googleSignIn(context: Context) = viewModelScope.launch {
        repository.googleSignIn(context).collectLatest { state ->
            _authState.update {
                it.copy(
                    state = state
                )
            }
        }
    }

    fun getCurrentUser() = repository.getCurrentUser()

    fun signOut() = viewModelScope.launch {
        repository.signOut()
    }
}