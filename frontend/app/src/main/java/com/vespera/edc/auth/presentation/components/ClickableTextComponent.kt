package com.vespera.edc.auth.presentation.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.sp

@Composable
fun ClickableTextComponent(
    unClickableText: String,
    clickableText: String,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth()
    ) {
        Text(
            text = unClickableText,
            style = TextStyle(
                color = MaterialTheme.colorScheme.primaryContainer,
                fontStyle = FontStyle.Normal,
                fontSize = 14.sp
            ),
        )
        Text(
            text = clickableText,
            style = TextStyle(
                color = MaterialTheme.colorScheme.primaryContainer,
                fontStyle = FontStyle.Normal,
                textDecoration = TextDecoration.Underline,
                fontWeight = FontWeight.Bold,
                fontSize = 14.sp,
            ),
            modifier = Modifier.clickable {
                onClick()
            }
        )
    }
}