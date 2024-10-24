package com.vespera.edc.auth.domain.repository

import android.content.Context
import com.google.firebase.auth.FirebaseUser
import com.vespera.edc.core.models.Resource
import com.vespera.edc.core.models.User
import kotlinx.coroutines.flow.Flow

interface AuthRepository {
    suspend fun register(user: User): Flow<Resource<FirebaseUser>>
    suspend fun logIn(user: User): Flow<Resource<FirebaseUser>>
    suspend fun googleSignIn(context: Context): Flow<Resource<FirebaseUser>>
    fun getCurrentUser(): FirebaseUser?
    suspend fun signOut()
}