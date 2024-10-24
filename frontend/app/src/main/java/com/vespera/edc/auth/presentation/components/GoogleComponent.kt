package com.vespera.edc.auth.presentation.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ElevatedButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun GoogleComponent(
    onClickGoogle: () -> Unit,
    modifier: Modifier = Modifier
) {
    ElevatedButton(
        onClick = {
            onClickGoogle()
        },
        modifier = modifier
            .fillMaxWidth()
            .height(56.dp),
        elevation = ButtonDefaults.elevatedButtonElevation(
            defaultElevation = 8.dp
        ),
        shape = RoundedCornerShape(10.dp),
        colors = ButtonColors(
            contentColor = MaterialTheme.colorScheme.primary,
            disabledContentColor = MaterialTheme.colorScheme.primary,
            disabledContainerColor = MaterialTheme.colorScheme.background,
            containerColor = MaterialTheme.colorScheme.background
        ),
        border = BorderStroke(
            width = 1.dp,
            color = MaterialTheme.colorScheme.primary
        ),
    ) {
//        Icon(painter = painterResource(id = R.drawable.google), contentDescription = "")
        Spacer(modifier = Modifier.width(10.dp))
        Text(text = "Sign in with Google")
    }
}