package com.vespera.edc.di

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import com.vespera.edc.auth.data.repository.AuthRepositoryImpl
import com.vespera.edc.auth.domain.repository.AuthRepository
import com.vespera.edc.auth.presentation.viewmodels.AuthViewModel
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import org.koin.core.module.dsl.viewModel
import org.koin.dsl.module
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit

object AppModule {
    val module = module {
        single<HttpLoggingInterceptor>{
            HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }
        }

        single<OkHttpClient>{
            OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.MINUTES)
                .readTimeout(10, TimeUnit.MINUTES)
                .writeTimeout(10, TimeUnit.MINUTES)
                .addInterceptor(get<HttpLoggingInterceptor>())
                .build()
        }

        single<Moshi> {
            Moshi.Builder()
                .add(KotlinJsonAdapterFactory())
                .build()
        }

        single<Retrofit>{
            Retrofit.Builder()
                .baseUrl("https://api.github.com/")
                .client(get<OkHttpClient>())
                .addConverterFactory(MoshiConverterFactory.create(get<Moshi>()))
                .build()
        }

        single<FirebaseAuth> {
            Firebase.auth
        }

        single<AuthRepository>{
            AuthRepositoryImpl(get<FirebaseAuth>())
        }

        viewModel<AuthViewModel> {
            AuthViewModel(get<AuthRepository>())
        }
    }
}