package com.vespera.edc.core.components

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

@Composable
fun HeadingTextComponent(
    text: String,
    modifier: Modifier = Modifier
) {
    Text(
        text = text,
        style = TextStyle(
            fontSize = 30.sp,
            fontWeight = FontWeight(700),
            color = MaterialTheme.colorScheme.primaryContainer
        ),
        modifier = modifier
    )
}