using System.Reflection;
using HarmonyLib;
using RimWorld;
using Verse;
using Verse.AI;

namespace RimFridgeWallAccessFix
{
    [StaticConstructorOnStartup]
    public static class Bootstrap
    {
        static Bootstrap()
        {
            new Harmony("ckvam.rimfridge.wallaccessfix").PatchAll(Assembly.GetExecutingAssembly());
            Log.Message("[RimFridge Wall Access Fix] Loaded.");
        }
    }

    internal static class RimFridgeWallAccess
    {
        private static FieldInfo currentTempField;
        private static FieldInfo roomsField;

        internal static bool IsThingInRimFridgeWallStorage(Thing thing)
        {
            if (thing == null || thing.MapHeld == null)
            {
                return false;
            }

            IntVec3 position = thing.PositionHeld;
            if (!position.IsValid)
            {
                return false;
            }

            var things = position.GetThingList(thing.MapHeld);
            for (int i = 0; i < things.Count; i++)
            {
                Thing candidate = things[i];
                ThingDef def = candidate?.def;
                if (def == null || def.passability != Traversability.Impassable)
                {
                    continue;
                }

                if (IsRimFridgeWallDef(def))
                {
                    return true;
                }
            }

            return false;
        }

        internal static bool TryGetSafeTemperature(object fridge, object comp, ref float result)
        {
            Thing thing = fridge as Thing;
            if (thing == null)
            {
                return false;
            }

            Room[] rooms = GetRooms(fridge);
            float totalTemperature = 0f;
            int roomCount = 0;

            if (rooms != null)
            {
                for (int i = 0; i < rooms.Length; i++)
                {
                    Room room = rooms[i];
                    if (room == null)
                    {
                        continue;
                    }

                    totalTemperature += room.Temperature;
                    roomCount++;
                }
            }

            if (roomCount > 0)
            {
                result = totalTemperature / roomCount;
                return true;
            }

            Map map = thing.MapHeld;
            if (map == null || !thing.PositionHeld.IsValid)
            {
                result = GetCurrentTemp(comp, 21f);
                return true;
            }

            RoofDef roof = thing.PositionHeld.GetRoof(map);
            result = roof == null ? map.mapTemperature.OutdoorTemp : GetCurrentTemp(comp, map.mapTemperature.OutdoorTemp);
            return true;
        }

        internal static bool TryPushSafeHeat(object fridge, float energy, object comp)
        {
            Thing thing = fridge as Thing;
            if (thing == null)
            {
                return false;
            }

            Room[] rooms = GetRooms(fridge);
            int roomCount = 0;

            if (rooms != null)
            {
                for (int i = 0; i < rooms.Length; i++)
                {
                    if (rooms[i] != null)
                    {
                        roomCount++;
                    }
                }
            }

            if (roomCount > 0)
            {
                float energyPerRoom = energy / roomCount;
                for (int i = 0; i < rooms.Length; i++)
                {
                    Room room = rooms[i];
                    if (room != null)
                    {
                        room.PushHeat(energyPerRoom);
                    }
                }

                return true;
            }

            Map map = thing.MapHeld;
            if (map == null || !thing.PositionHeld.IsValid)
            {
                return true;
            }

            RoofDef roof = thing.PositionHeld.GetRoof(map);
            if (roof != null)
            {
                SetCurrentTemp(comp, GetCurrentTemp(comp, map.mapTemperature.OutdoorTemp) + energy + 1f);
            }

            return true;
        }

        private static bool IsRimFridgeWallDef(ThingDef def)
        {
            if (def == null)
            {
                return false;
            }

            string defName = def.defName ?? string.Empty;
            string thingClass = def.thingClass == null ? string.Empty : def.thingClass.FullName;
            return defName.StartsWith("RimFridge_", System.StringComparison.Ordinal)
                && defName.IndexOf("Wall", System.StringComparison.OrdinalIgnoreCase) >= 0
                && thingClass.IndexOf("RimFridge", System.StringComparison.OrdinalIgnoreCase) >= 0;
        }

        private static Room[] GetRooms(object fridge)
        {
            if (fridge == null)
            {
                return null;
            }

            if (roomsField == null)
            {
                roomsField = AccessTools.Field(fridge.GetType(), "rooms");
            }

            return roomsField == null ? null : roomsField.GetValue(fridge) as Room[];
        }

        private static float GetCurrentTemp(object comp, float fallback)
        {
            if (comp == null)
            {
                return fallback;
            }

            FieldInfo field = GetCurrentTempField(comp);
            if (field == null)
            {
                return fallback;
            }

            object value = field.GetValue(comp);
            return value is float ? (float)value : fallback;
        }

        private static void SetCurrentTemp(object comp, float value)
        {
            FieldInfo field = GetCurrentTempField(comp);
            if (field != null)
            {
                field.SetValue(comp, value);
            }
        }

        private static FieldInfo GetCurrentTempField(object comp)
        {
            if (comp == null)
            {
                return null;
            }

            if (currentTempField == null)
            {
                currentTempField = AccessTools.Field(comp.GetType(), "currentTemp");
            }

            return currentTempField;
        }
    }

    [HarmonyPatch]
    internal static class RimFridgeBuildingGetTemperaturePatch
    {
        private static MethodBase TargetMethod()
        {
            return AccessTools.Method(AccessTools.TypeByName("RimFridge.RimFridge_Building"), "GetTemperatureOfSurroundings");
        }

        private static bool Prefix(object __instance, object comp, ref float __result)
        {
            return !RimFridgeWallAccess.TryGetSafeTemperature(__instance, comp, ref __result);
        }
    }

    [HarmonyPatch]
    internal static class RimFridgeBuildingPushHeatPatch
    {
        private static MethodBase TargetMethod()
        {
            return AccessTools.Method(AccessTools.TypeByName("RimFridge.RimFridge_Building"), "PushTransferredAndGeneratedHeat");
        }

        private static bool Prefix(object __instance, float energy, object comp)
        {
            return !RimFridgeWallAccess.TryPushSafeHeat(__instance, energy, comp);
        }
    }

    [HarmonyPatch]
    internal static class RimFridgeWallBuildingGetTemperaturePatch
    {
        private static MethodBase TargetMethod()
        {
            return AccessTools.Method(AccessTools.TypeByName("RimFridge.RimFridge_WallBuilding"), "GetTemperatureOfSurroundings");
        }

        private static bool Prefix(object __instance, object comp, ref float __result)
        {
            return !RimFridgeWallAccess.TryGetSafeTemperature(__instance, comp, ref __result);
        }
    }

    [HarmonyPatch]
    internal static class RimFridgeWallBuildingPushHeatPatch
    {
        private static MethodBase TargetMethod()
        {
            return AccessTools.Method(AccessTools.TypeByName("RimFridge.RimFridge_WallBuilding"), "PushTransferredAndGeneratedHeat");
        }

        private static bool Prefix(object __instance, float energy, object comp)
        {
            return !RimFridgeWallAccess.TryPushSafeHeat(__instance, energy, comp);
        }
    }

    [HarmonyPatch(typeof(Pawn_PathFollower), nameof(Pawn_PathFollower.StartPath))]
    internal static class PawnPathFollowerStartPathPatch
    {
        private static void Prefix(LocalTargetInfo dest, ref PathEndMode peMode)
        {
            if (peMode != PathEndMode.OnCell || !dest.HasThing)
            {
                return;
            }

            if (RimFridgeWallAccess.IsThingInRimFridgeWallStorage(dest.Thing))
            {
                peMode = PathEndMode.Touch;
            }
        }
    }

    [HarmonyPatch(typeof(WorkGiver_ExtractSkull), nameof(WorkGiver_ExtractSkull.HasJobOnThing))]
    internal static class WorkGiverExtractSkullHasJobOnThingPatch
    {
        private static void Postfix(Pawn pawn, Thing t, bool forced, ref bool __result)
        {
            if (!__result || !RimFridgeWallAccess.IsThingInRimFridgeWallStorage(t))
            {
                return;
            }

            if (!pawn.CanReach(t, PathEndMode.Touch, Danger.Deadly))
            {
                __result = false;
            }
        }
    }
}
