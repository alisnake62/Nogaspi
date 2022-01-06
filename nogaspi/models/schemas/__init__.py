from .register import LoginInputSchema, CheckTokenValidityInputSchema
from .food import (
    GetProductInputSchema,
    PostDonationFromScanInputSchema,
    PostDonationFromFridgeInputSchema,
    DeleteMyDonationsInputSchema,
    GetDonationsInputSchema,
    GetDonationsByRegularPathInputSchema,
    GetAllergensInputSchema,
    PostArticlesInFridgeInputSchema,
    DeleteArticlesInFridgeInputSchema,
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