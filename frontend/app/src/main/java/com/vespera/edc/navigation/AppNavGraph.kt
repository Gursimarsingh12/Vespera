package com.vespera.edc.navigation

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.vespera.edc.auth.presentation.screens.HomeScreen
import com.vespera.edc.auth.presentation.screens.SignUpScreen
import com.vespera.edc.auth.presentation.viewmodels.AuthViewModel
import org.koin.androidx.compose.koinViewModel

@Composable
fun AppNavGraph(
    authViewModel: AuthViewModel = koinViewModel(),
    context: Context
) {
    val navController = rememberNavController()
    val startDestination = if(authViewModel.getCurrentUser() != null){
        Screens.HomeScreen
    }else{
        Screens.SignUpScreen
    }
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable<Screens.SignUpScreen> {
            SignUpScreen(
                navigateToHomeScreen = {
                    navController.navigate(Screens.HomeScreen)
                },
                navigateToLogInScreen = {

                },
                authViewModel = authViewModel,
                context = context
            )
        }
        composable<Screens.HomeScreen> {
            HomeScreen()
        }
    }
}