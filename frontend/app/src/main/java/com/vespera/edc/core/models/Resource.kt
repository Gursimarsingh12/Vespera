package com.vespera.edc.core.models

sealed class Resource<out T> {
    data object Idle : Resource<Nothing>()
    data object Loading : Resource<Nothing>()
    data class Error(val message: String?) : Resource<Nothing>()
    data class Success<T>(val data: T?) : Resource<T>()
}