package com.vespera.edc.auth.data.repository

import android.content.Context
import android.util.Log
import androidx.credentials.CredentialManager
import androidx.credentials.GetCredentialRequest
import androidx.credentials.exceptions.GetCredentialCancellationException
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseAuthException
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.GoogleAuthProvider
import com.vespera.edc.R
import com.vespera.edc.auth.domain.repository.AuthRepository
import com.vespera.edc.core.models.Resource
import com.vespera.edc.core.models.User
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.tasks.await

class AuthRepositoryImpl(
    private val auth: FirebaseAuth,
): AuthRepository {
    override suspend fun register(user: User): Flow<Resource<FirebaseUser>> = flow {
        emit(Resource.Loading)
        try {
            val result = auth.createUserWithEmailAndPassword(user.email!!, user.password!!).await()
            emit(Resource.Success(result.user))
        }catch (e: Exception){
            Log.d(TAG, e.localizedMessage ?: "An unknown error occurred")
            emit(Resource.Error(e.message ?: "An unknown error occurred"))
        }
    }

    override suspend fun logIn(user: User): Flow<Resource<FirebaseUser>> = flow {
        emit(Resource.Loading)
        try {
            val result = auth.signInWithEmailAndPassword(
                user.email!!,
                user.password!!
            ).await()
            emit(Resource.Success(data = result.user))
        } catch (e: Exception) {
            emit(Resource.Error(e.localizedMessage ?: "An unknown error occurred"))
        }
    }

    override suspend fun googleSignIn(context: Context): Flow<Resource<FirebaseUser>> = flow {
        emit(Resource.Loading)
        try {
            val credentialManager = CredentialManager.create(context)
            val request = googleClientRequest(context)
            val result = credentialManager.getCredential(
                context = context,
                request = request
            )
            val credential = result.credential
            val googleIdToken = GoogleIdTokenCredential.createFrom(credential.data).idToken

            val firebaseCredential = GoogleAuthProvider.getCredential(googleIdToken, null)
            val authResult = auth.signInWithCredential(firebaseCredential).await()
            emit(Resource.Success(authResult.user))
        }catch (_: GetCredentialCancellationException) {
            emit(Resource.Idle)
        } catch (e: FirebaseAuthException) {
            emit(Resource.Error(e.localizedMessage ?: "An unknown error occurred"))
        } catch (e: Exception) {
            emit(Resource.Error(e.message ?: "An unknown error occurred"))
        }
    }

    override fun getCurrentUser(): FirebaseUser? = auth.currentUser

    override suspend fun signOut() = auth.signOut()

    private fun googleClientRequest(context: Context): GetCredentialRequest {
        val googleIdOption = GetGoogleIdOption.Builder()
            .setFilterByAuthorizedAccounts(false)
            .setServerClientId(context.getString(R.string.default_web_client_id))
            .setAutoSelectEnabled(false)
            .build()
        val request = GetCredentialRequest.Builder()
            .addCredentialOption(googleIdOption)
            .build()
        return request
    }

    companion object{
        const val TAG = "AuthRepositoryImpl"
    }
}