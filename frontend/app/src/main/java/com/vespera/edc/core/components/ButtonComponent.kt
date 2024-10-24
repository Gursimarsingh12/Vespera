package com.vespera.edc.core.components

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ElevatedButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun ButtonComponent(
    modifier: Modifier = Modifier,
    onClickAction: () -> Unit,
    buttonText: String
) {
    ElevatedButton(
        onClick = {
            onClickAction()
        },
        colors = ButtonColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer,
            disabledContainerColor = MaterialTheme.colorScheme.primaryContainer,
            disabledContentColor = MaterialTheme.colorScheme.background,
            contentColor = MaterialTheme.colorScheme.background
        ),
        shape = RoundedCornerShape(13.dp),
        elevation = ButtonDefaults.elevatedButtonElevation(
            defaultElevation = 10.dp
        ),
        modifier = modifier
            .fillMaxWidth()
            .height(56.dp)
    ) {
        Text(
            text = buttonText,
            fontWeight = FontWeight.Bold
        )
    }
}