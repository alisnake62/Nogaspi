from .register import LoginInputSchema, CheckTokenValidityInputSchema
from .food import (
    GetProductInputSchema,
    PostDonationFromScanInputSchema,
    PostDonationFromFridgeInputSchema,
    GetDonationsInputSchema,
    GetDonationsByRegularPathinputSchema,
    GetAllergensInputSchema,
    PostArticlesInFridgeInputSchema,
    GetArticlesInFridgeInputSchema,
    TakeDonationInputSchema,
    GetDonationCodeInputSchema,
    GetFavoriteDonationsInputSchema,
    ToggleDonationInMyFavoriteInputSchema,
    GetMyDonationCodeInputSchema,
)
from .user import (
    PostRegularPathInputSchema,
    GetRegularPathInputSchema
)