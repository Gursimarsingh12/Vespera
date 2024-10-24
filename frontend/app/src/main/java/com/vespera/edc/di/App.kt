package com.vespera.edc.di

import android.app.Application
import org.koin.android.ext.koin.androidContext
import org.koin.android.ext.koin.androidLogger
import org.koin.core.context.startKoin
import org.koin.core.context.stopKoin
import org.koin.core.logger.Level
import org.koin.dsl.koinApplication

class App: Application() {
    private val app = koinApplication {
        modules(AppModule.module)
        androidContext(this@App)
        androidLogger(level = Level.DEBUG)
    }

    override fun onCreate() {
        super.onCreate()
        startKoin(app)
    }

    override fun onTerminate() {
        super.onTerminate()
        stopKoin()
    }
}